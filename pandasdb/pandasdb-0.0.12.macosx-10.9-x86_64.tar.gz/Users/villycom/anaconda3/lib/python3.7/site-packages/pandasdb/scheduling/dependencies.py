from airflow.sensors.external_task import ExternalTaskSensor, ExternalTaskMarker


def waiting_for(dag_id, parent_dag_ids, timeout=600, allowed_states=['success'], failed_states=['failed', 'skipped'],
                mode="reschedule"):
    tasks = []
    for parent_id in parent_dag_ids:
        tasks.append(ExternalTaskSensor(
            task_id=f"link.{parent_id}.{dag_id}",
            external_dag_id=parent_id,
            external_task_id=f"link.{parent_id}.{dag_id}",
            timeout=timeout,
            allowed_states=allowed_states,
            failed_states=failed_states,
            mode=mode,
        ))
    return tasks


def awaited_by(dag_id, child_dag_ids):
    tasks = []
    for child_id in child_dag_ids:
        tasks.append(ExternalTaskMarker(
            task_id=f"link.{dag_id}.{child_id}",
            external_dag_id=child_id,
            external_task_id=f"link.{dag_id}.{child_id}",
        ))
    return tasks
