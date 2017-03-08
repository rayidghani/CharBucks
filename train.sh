python /tensorflow/tensorflow/examples/image_retraining/retrain.py \
--bottleneck_dir=/CharBucks/latteart/bottlenecks \
--how_many_training_steps 4000 \
--model_dir=/CharBucks/latteart/inception \
--output_graph=/CharBucks/latteart/retrained_graph.pb \
--output_labels=/CharBucks/latteart/retrained_labels.txt \
--image_dir /CharBucks/latteart/data
