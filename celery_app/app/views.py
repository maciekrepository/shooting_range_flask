from flask import Blueprint, request, jsonify, Response, redirect, url_for
from flask.views import View, MethodView
from .task import send_mail_message


class SendMail(MethodView):
    def post(self):
        body = request.json
        task = send_mail_message.delay(body)
        print(redirect(url_for("TaskStatus", task_id=task.id)))
        return redirect(url_for("TaskStatus", task_id=task.id))
        # return 'Success'
        # return result_schema.jsonify(edited_result)


class TaskStatus(MethodView):
    """
    Used to retrieve current celery task status.
    """

    def get(self, task_id) -> dict:
        task = celery_app.AsyncResult(task_id)
        print(f"TASK STATUS: {task.status}")
        result = {"task_status": task.status}
        return result
