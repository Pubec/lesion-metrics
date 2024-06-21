## Lesion metrics

Original Repository: [https://github.com/jcreinhold/lesion-metrics](https://github.com/jcreinhold/lesion-metrics)

Improved:

- `pymedio` imports
- `helper.Metrics` **LTPR** bug
- `helper.Metrics` prettifed print


Various metrics for evaluating lesion segmentations [1]

## Install

The easiest way to install the package is with::

```bash
    pip install lesion-metrics pymedio
```

To install the dependencies of the CLI, install with::

```bash
    pip install "lesion-metrics[cli]"
```

You can also download the source and run::

```bash
    python setup.py install
```

## Basic Usage

You can generate a report of lesion metrics for a directory of predicted labels and truth labels
with the CLI:

```bash
    lesion-metrics -p predictions/ -t truth/ -o output.csv
```

Or you can import the metrics and run them on label images:

```python
import nibabel as nib
from lesion_metrics.metrics import dice

pred = nib.load('pred_label.nii.gz').get_fdata()
truth = nib.load('truth_label.nii.gz').get_fdata()
dice_score = dice(pred, truth)
```

```python
from lesion_metrics.helper import Metrics

metrics_5 = Metrics.from_filenames(pred_filename=path_pred, truth_filename=path_true, iou_threshold=0.05)
metrics_25 = Metrics.from_filenames(pred_filename=path_pred, truth_filename=path_true, iou_threshold=0.25)

print(metrics_5)
print(metrics_25)

```

