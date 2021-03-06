optimizer = dict(
    type='SGD',
    lr=0.01,
    momentum=0.9,
    weight_decay=0.0005,
    nesterov=True,
    paramwise_cfg=dict(norm_decay_mult=0.0, bias_decay_mult=0.0))
optimizer_config = dict(grad_clip=None)
lr_config = dict(
    policy='YOLOX',
    warmup='exp',
    by_epoch=False,
    warmup_by_epoch=True,
    warmup_ratio=1,
    warmup_iters=5,
    num_last_epochs=15,
    min_lr_ratio=0.05)
runner = dict(type='EpochBasedRunner', max_epochs=12)
checkpoint_config = dict(interval=4)
log_config = dict(interval=50, hooks=[dict(type='TextLoggerHook')])
custom_hooks = [
    dict(type='YOLOXModeSwitchHook', num_last_epochs=15, priority=48),
    dict(
        type='SyncRandomSizeHook',
        ratio_range=(10, 20),
        img_scale=(320, 320),
        priority=48),
    dict(type='SyncNormHook', num_last_epochs=15, interval=10, priority=48),
    dict(type='ExpMomentumEMAHook', resume_from=None, priority=49)
]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = './checkpoints/yolox_tiny_8x8_300e_coco_20210806_234250-4ff3b67e.pth'
resume_from = None
workflow = [('train', 1)]
model = dict(
    type='YOLOX',
    backbone=dict(type='CSPDarknet', deepen_factor=0.33, widen_factor=0.375),
    neck=dict(
        type='YOLOXPAFPN',
        in_channels=[96, 192, 384],
        out_channels=96,
        num_csp_blocks=1),
    bbox_head=dict(
        type='YOLOXHead', num_classes=5, in_channels=96, feat_channels=96),
    train_cfg=dict(assigner=dict(type='SimOTAAssigner', center_radius=2.5)),
    test_cfg=dict(score_thr=0.01, nms=dict(type='nms', iou_threshold=0.65)))
data_root = 'data/coco/'
dataset_type = 'CocoDataset'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
img_scale = (320, 320)
train_pipeline = [
    dict(type='Mosaic', img_scale=(320, 320), pad_val=84),
    dict(
        type='RandomAffine',
        scaling_ratio_range=(0.5, 1.5),
        border=(-320, -320)),
    dict(
        type='PhotoMetricDistortion',
        brightness_delta=32,
        contrast_range=(0.5, 1.5),
        saturation_range=(0.5, 1.5),
        hue_delta=18),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Resize', keep_ratio=True),
    dict(type='Pad', pad_to_square=True, pad_val=84),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
]
train_dataset = dict(
    type='MultiImageMixDataset',
    dataset=dict(
        type='CocoDataset',
        ann_file=
        '/home/kkb/mmdetection-master/Datasets/trainData/annotations/instances_train_images.json',
        img_prefix='/home/kkb/mmdetection-master/Datasets/trainData/images/val',
        pipeline=[
            dict(type='LoadImageFromFile', to_float32=True),
            dict(type='LoadAnnotations', with_bbox=True)
        ],
        filter_empty_gt=False),
    pipeline=[
        dict(type='Mosaic', img_scale=(320, 320), pad_val=84),
        dict(
            type='RandomAffine',
            scaling_ratio_range=(0.5, 1.5),
            border=(-320, -320)),
        dict(
            type='PhotoMetricDistortion',
            brightness_delta=32,
            contrast_range=(0.5, 1.5),
            saturation_range=(0.5, 1.5),
            hue_delta=18),
        dict(type='RandomFlip', flip_ratio=0.5),
        dict(type='Resize', keep_ratio=True),
        dict(type='Pad', pad_to_square=True, pad_val=84),
        dict(
            type='Normalize',
            mean=[123.675, 116.28, 103.53],
            std=[58.395, 57.12, 57.375],
            to_rgb=True),
        dict(type='DefaultFormatBundle'),
        dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
    ],
    dynamic_scale=(320, 320))
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(300, 300),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Pad', size=(300, 300), pad_val=84),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=8,
    workers_per_gpu=2,
    train=dict(
        type='MultiImageMixDataset',
        dataset=dict(
            type='CocoDataset',
            ann_file=
            '/home/kkb/mmdetection-master/Datasets/trainData/annotations/instances_train_images.json',
            img_prefix=
            '/home/kkb/mmdetection-master/Datasets/trainData/images/train',
            pipeline=[
                dict(type='LoadImageFromFile', to_float32=True),
                dict(type='LoadAnnotations', with_bbox=True)
            ],
            filter_empty_gt=False),
        pipeline=[
            dict(type='Mosaic', img_scale=(320, 320), pad_val=84),
            dict(
                type='RandomAffine',
                scaling_ratio_range=(0.5, 1.5),
                border=(-320, -320)),
            dict(
                type='PhotoMetricDistortion',
                brightness_delta=32,
                contrast_range=(0.5, 1.5),
                saturation_range=(0.5, 1.5),
                hue_delta=18),
            dict(type='RandomFlip', flip_ratio=0.5),
            dict(type='Resize', keep_ratio=True),
            dict(type='Pad', pad_to_square=True, pad_val=84),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels'])
        ],
        dynamic_scale=(320, 320)),
    val=dict(
        type='CocoDataset',
        ann_file=
        '/home/kkb/mmdetection-master/Datasets/trainData/annotations/instances_val_images.json',
        img_prefix='/home/kkb/mmdetection-master/Datasets/trainData/images/val',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(300, 300),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(type='Pad', size=(300, 300), pad_val=84),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='DefaultFormatBundle'),
                    dict(type='Collect', keys=['img'])
                ])
        ]),
    test=dict(
        type='CocoDataset',
        ann_file=
        '/home/kkb/mmdetection-master/Datasets/trainData/annotations/instances_val_images.json',
        img_prefix='/home/kkb/mmdetection-master/Datasets/trainData/images/val',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(300, 300),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(type='Pad', size=(300, 300), pad_val=84),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='DefaultFormatBundle'),
                    dict(type='Collect', keys=['img'])
                ])
        ]))
interval = 10
evaluation = dict(interval=10, metric='bbox')
work_dir = './work_dirs/yolox_tiny_8x8_300e_coco'
gpu_ids = range(0, 1)
