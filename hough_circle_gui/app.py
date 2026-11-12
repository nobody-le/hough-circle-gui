"""Tkinter user interface for Hough circle detection."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import cv2
import numpy as np
from PIL import Image, ImageTk

from .detector import HoughParams, annotate_image, detect_circles
from .presets import COINS, COOKIE_PLATE, generic_params, preset_for_path

PRESET_BY_LABEL = {"Coins": COINS, "Cookie Plate": COOKIE_PLATE}
SLIDER_SPECS = (
    ("dp", "dp", 1.0, 3.0, 0.1),
    ("min_dist", "minDist", 10, 800, 1),
    ("param1", "param1", 10, 300, 1),
    ("param2", "param2", 5, 150, 1),
    ("min_radius", "minRadius", 0, 600, 1),
    ("max_radius", "maxRadius", 1, 600, 1),
)


class HoughCircleApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Hough Circle Detector")
        self.root.geometry("1200x760")
        self.root.minsize(960, 620)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.image: np.ndarray | None = None
        self.annotated: np.ndarray | None = None
        self.circles: list[tuple[int, int, int]] = []
        self.current_path: Path | None = None
        self._photo: ImageTk.PhotoImage | None = None
        self._debounce_id: str | None = None
        self._setting_params = False

        self.param_vars: dict[str, tk.Variable] = {
            "dp": tk.DoubleVar(value=1.2),
            "min_dist": tk.IntVar(value=250),
            "param1": tk.IntVar(value=100),
            "param2": tk.IntVar(value=30),
            "min_radius": tk.IntVar(value=120),
            "max_radius": tk.IntVar(value=200),
        }
        self.preset_var = tk.StringVar(value="Auto")
        self.status_var = tk.StringVar(value="No image loaded")

        self._build_ui()
        self._set_params(generic_params(760, 385))

    def _build_ui(self) -> None:
        controls = ttk.Frame(self.root, padding=10)
        controls.grid(row=0, column=0, sticky="ns")

        ttk.Label(
            controls, text="Hough Circle Detector", font=("TkDefaultFont", 14, "bold")
        ).pack(anchor="w", pady=(0, 8))

        ttk.Button(controls, text="Open Image", command=self.open_image).pack(
            fill="x", pady=2
        )

        sample_row = ttk.Frame(controls)
        sample_row.pack(fill="x", pady=2)
        ttk.Button(
            sample_row,
            text="Coins Sample",
            command=lambda: self.load_sample("coins.jpg"),
        ).pack(side="left", expand=True, fill="x", padx=(0, 2))
        ttk.Button(
            sample_row,
            text="Plate Sample",
            command=lambda: self.load_sample("cookie-plate.jpg"),
        ).pack(side="left", expand=True, fill="x", padx=(2, 0))

        ttk.Label(controls, text="Preset").pack(anchor="w", pady=(10, 0))
        self.preset_box = ttk.Combobox(
            controls,
            textvariable=self.preset_var,
            values=["Auto", "Coins", "Cookie Plate", "Custom"],
            state="readonly",
        )
        self.preset_box.pack(fill="x", pady=(2, 8))
        self.preset_box.bind("<<ComboboxSelected>>", self._on_preset_selected)

        for key, label, low, high, resolution in SLIDER_SPECS:
            scale = tk.Scale(
                controls,
                label=label,
                from_=low,
                to=high,
                resolution=resolution,
                orient=tk.HORIZONTAL,
                length=250,
                variable=self.param_vars[key],
                command=self._on_param_change,
            )
            scale.pack(fill="x", pady=1)

        ttk.Button(controls, text="Detect", command=self._run_detection).pack(
            fill="x", pady=(10, 2)
        )
        ttk.Button(
            controls, text="Export Annotated", command=self.export_image
        ).pack(fill="x", pady=2)
        ttk.Button(controls, text="Reset Params", command=self._reset_params).pack(
            fill="x", pady=2
        )

        preview = ttk.Frame(self.root, padding=(0, 10, 10, 0))
        preview.grid(row=0, column=1, sticky="nsew")
        preview.columnconfigure(0, weight=1)
        preview.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(preview, bg="#202124", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        ttk.Label(
            self.root,
            textvariable=self.status_var,
            anchor="w",
            relief="sunken",
            padding=4,
        ).grid(row=1, column=0, columnspan=2, sticky="ew")

    def open_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Open image",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self.load_image(path)

    def load_sample(self, filename: str) -> None:
        sample = Path(__file__).resolve().parent.parent / "examples" / filename
        self.load_image(sample)

    def load_image(self, path: str | Path) -> bool:
        path = Path(path)
        try:
            data = np.fromfile(str(path), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        except OSError as exc:
            messagebox.showerror("Open image", f"Cannot read image:\n{exc}")
            return False

        if image is None:
            messagebox.showerror("Open image", f"Cannot decode image:\n{path}")
            return False

        self.image = image
        self.annotated = None
        self.circles = []
        self.current_path = path

        preset = preset_for_path(path)
        if preset is COINS:
            self.preset_var.set("Coins")
            self._set_params(preset.params)
        elif preset is COOKIE_PLATE:
            self.preset_var.set("Cookie Plate")
            self._set_params(preset.params)
        else:
            self.preset_var.set("Auto")
            self._set_params(generic_params(image.shape[1], image.shape[0]))

        self._render()
        self._run_detection()
        return True

    def _on_preset_selected(self, _event: tk.Event | None = None) -> None:
        preset = PRESET_BY_LABEL.get(self.preset_var.get())
        if preset is not None:
            self._set_params(preset.params)
            self._run_detection()
        elif self.preset_var.get() == "Auto" and self.image is not None:
            self._set_params(generic_params(self.image.shape[1], self.image.shape[0]))
            self._run_detection()

    def _set_params(self, params: HoughParams) -> None:
        self._setting_params = True
        try:
            for key, var in self.param_vars.items():
                var.set(getattr(params, key))
        finally:
            self._setting_params = False

    def _read_params(self) -> HoughParams | None:
        try:
            return HoughParams(
                dp=float(self.param_vars["dp"].get()),
                min_dist=int(self.param_vars["min_dist"].get()),
                param1=int(self.param_vars["param1"].get()),
                param2=int(self.param_vars["param2"].get()),
                min_radius=int(self.param_vars["min_radius"].get()),
                max_radius=int(self.param_vars["max_radius"].get()),
            )
        except (tk.TclError, ValueError) as exc:
            self.status_var.set(f"Invalid parameters: {exc}")
            return None

    def _on_param_change(self, _value: str | None = None) -> None:
        if self._setting_params:
            return
        self.preset_var.set("Custom")
        if self._debounce_id is not None:
            self.root.after_cancel(self._debounce_id)
        self._debounce_id = self.root.after(150, self._run_detection)

    def _run_detection(self) -> None:
        self._debounce_id = None
        if self.image is None:
            return

        params = self._read_params()
        if params is None:
            return

        try:
            circles = detect_circles(self.image, params)
            annotated = annotate_image(self.image, circles)
        except Exception as exc:
            self.status_var.set(f"Detection failed: {exc}")
            return

        self.circles = circles
        self.annotated = annotated
        self._render()

        name = self.current_path.name if self.current_path else "image"
        height, width = self.image.shape[:2]
        self.status_var.set(
            f"{name} | {width}x{height} | circles: {len(circles)} | "
            f"dp={params.dp:.1f} minDist={params.min_dist} "
            f"p1={params.param1} p2={params.param2} "
            f"r={params.min_radius}-{params.max_radius}"
        )

    def _reset_params(self) -> None:
        if self.image is None:
            self._set_params(generic_params(760, 385))
        else:
            height, width = self.image.shape[:2]
            self._set_params(generic_params(width, height))
        self.preset_var.set("Auto")
        self._run_detection()

    def _render(self) -> None:
        source = self.annotated if self.annotated is not None else self.image
        if source is None:
            self.canvas.delete("all")
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 10 or canvas_height < 10:
            canvas_width = source.shape[1]
            canvas_height = source.shape[0]

        scale = min(
            canvas_width / source.shape[1],
            canvas_height / source.shape[0],
            1.0,
        )
        target_size = (
            max(1, int(source.shape[1] * scale)),
            max(1, int(source.shape[0] * scale)),
        )
        rgb = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)
        if pil_image.size != target_size:
            pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)

        self._photo = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self._photo,
            anchor="center",
        )

    def _on_canvas_resize(self, _event: tk.Event | None = None) -> None:
        self._render()

    def export_image(self) -> None:
        if self.annotated is None:
            messagebox.showinfo("Export", "Load and detect an image first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export annotated image",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg")],
        )
        if path:
            self.export_annotated(path)

    def export_annotated(self, path: str | Path) -> bool:
        if self.annotated is None:
            return False

        path = Path(path)
        try:
            rgb = cv2.cvtColor(self.annotated, cv2.COLOR_BGR2RGB)
            Image.fromarray(rgb).save(path)
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))
            self.status_var.set(f"Export failed: {exc}")
            return False

        self.status_var.set(f"Exported {path.name} | circles: {len(self.circles)}")
        return True


def main() -> None:
    root = tk.Tk()
    HoughCircleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
