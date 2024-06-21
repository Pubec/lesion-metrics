"""Evaluate all metrics on a pair of lesion segmentations
Author: Jacob Reinhold
"""

from __future__ import annotations

import builtins
import dataclasses

import pymedio.image as mioi

import lesion_metrics.metrics as lmm
import lesion_metrics.typing as lmt
import lesion_metrics.volume as lmv


@dataclasses.dataclass
class Metrics:
    avd: float
    dice: float
    isbi15_score: float
    jaccard: float
    lfdr: float
    ltpr: float
    ppv: float
    tpr: float
    truth_volume: float
    pred_volume: float
    truth_count: int
    pred_count: int
    iou_threshold: float = None

    @classmethod
    def from_filenames(
        cls,
        pred_filename: lmt.PathLike,
        truth_filename: lmt.PathLike,
        *,
        iou_threshold: builtins.float = 0.0
    ) -> Metrics:
        assert 0.0 <= iou_threshold < 1.0
        pred = mioi.Image.from_path(pred_filename)
        truth = mioi.Image.from_path(truth_filename)
        _avd = lmm.avd(pred, truth)
        dc = lmm.dice(pred, truth)
        jc = lmm.jaccard(pred, truth)
        __lfdr = lmm.lfdr(
            pred, truth, iou_threshold=iou_threshold, return_pred_count=True
        )
        assert isinstance(__lfdr, tuple)
        _lfdr, np = __lfdr
        __ltpr = lmm.ltpr(
            pred, truth, iou_threshold=iou_threshold, return_truth_count=True
        )
        assert isinstance(__ltpr, tuple)
        _ltpr, nt = __ltpr
        _ppv = lmm.ppv(pred, truth)
        _tpr = lmm.tpr(pred, truth)
        isbi15 = lmm.isbi15_score_from_metrics(dc, _ppv, _lfdr, _ltpr)
        vol_t = lmv.SegmentationVolume(truth).volume()
        vol_p = lmv.SegmentationVolume(pred).volume()
        return Metrics(
            avd=_avd,
            dice=dc,
            isbi15_score=isbi15,
            jaccard=jc,
            lfdr=_lfdr,
            ltpr=_ltpr,
            ppv=_ppv,
            tpr=_tpr,
            truth_volume=vol_t,
            pred_volume=vol_p,
            truth_count=nt,
            pred_count=np,
            iou_threshold=iou_threshold
        )


    def __str__(self):
        return (
            f"Metrics:\n"
            f"  AVD: {self.avd}\n"
            f"  Dice: {self.dice}\n"
            f"  ISBI15 Score: {self.isbi15_score}\n"
            f"  Jaccard: {self.jaccard}\n"
            f"  LFDR: {self.lfdr}\n"
            f"  LTPR: {self.ltpr}\n"
            f"  PPV: {self.ppv}\n"
            f"  TPR: {self.tpr}\n"
            f"  Truth Volume: {self.truth_volume}\n"
            f"  Pred Volume: {self.pred_volume}\n"
            f"  Truth Count: {self.truth_count}\n"
            f"  Pred Count: {self.pred_count}\n"
            f"  Threshold: {self.iou_threshold}\n"
        )