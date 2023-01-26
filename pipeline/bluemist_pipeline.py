from joblib import dump

pipeline_steps = {}
pipelines = {}


def save_preprocessor(preprocessor):
    dump(preprocessor, 'artifcats/preprocessor/preprocessor.joblib')
    print('preprocessor', preprocessor)


def add_pipeline_step(estimator_name, pipeline_step):
    if estimator_name not in pipeline_steps:
        pipeline_steps[estimator_name] = []

    if estimator_name in pipeline_steps:
        steps = pipeline_steps[estimator_name]
        steps.append(pipeline_step)
        print(steps)
        return steps


def save_pipeline(estimator_name, pipeline):
    pipelines[estimator_name] = pipeline
    dump(pipeline, 'artifcats/models/' + estimator_name + '.joblib')
    print(pipelines)
