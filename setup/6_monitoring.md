## Model monitoring

We'll use `Evidently` for model monitoring. It offers interactive reports so you may track your model's behavior over time. Additionally, it offers a collection of measures for identifying data drift and model performance drift. To keep track of the model performance, we'll build a dashboard using `Grafana`.

Since a model has previously been trained using the training data, model monitoring operates on this premise. New data will, nevertheless, be produced over time. We want to use the additional data to track data drift and model performance. We will retrain the model if both the data drift and model performance are outside of the threshold.

In evidently, `referenced data` is the data that was used to train the model. The `current data` is the new data that is generated over time. The `current data` is used to monitor the model performance and data drift.

First, change directory to `monitor` folder

```bash
cd ~/cyberbullying_detection/monitoring
```

Run `produce` to send data to our streaming service. 

```bash
python produce.py
```

Run `consume` to consume resulted data from our streaming service and save data as `current.csv` in the sub-folder `data`

```bash
python consume.py
```

To view the model monitoring dashboard, run the following command:
```bash
docker-compose up
```

Generate `evidently` report and tracking database for `grafana` monitoring dashboard

```bash
python evidently_grafana_metrics.py
```

You can view the dashboard on the following URL. Note: Allow port 3000 for port forwarding in VS Code.
```bash
http://localhost:3000
```

The dashboard will look like the following. The dashboard provides metrics such as `Accuracy`, `Precision`, `Recall`, and `F1 Score`.

![grafana](../images/grafana.png)
