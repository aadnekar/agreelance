# Generated by Django 2.1.7 on 2020-01-16 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(related_name="teams", to="user.Profile"),
        ),
        migrations.AddField(
            model_name="team",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="projects.Task",
            ),
        ),
        migrations.AddField(
            model_name="taskoffer",
            name="offerer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="taskoffer",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="projects.Task"
            ),
        ),
        migrations.AddField(
            model_name="taskfileteam",
            name="file",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="projects.TaskFile",
            ),
        ),
        migrations.AddField(
            model_name="taskfileteam",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="file",
                to="projects.Team",
            ),
        ),
        migrations.AddField(
            model_name="taskfile",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="projects.Task",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="modify",
            field=models.ManyToManyField(
                related_name="task_participants_modify", to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="projects.Project",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="read",
            field=models.ManyToManyField(
                related_name="task_participants_read", to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="write",
            field=models.ManyToManyField(
                related_name="task_participants_write", to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_category",
                to="projects.ProjectCategory",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="participants",
            field=models.ManyToManyField(
                related_name="project_participants", to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user.Profile"
            ),
        ),
        migrations.AddField(
            model_name="delivery",
            name="delivery_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="deliveries",
                to="user.Profile",
            ),
        ),
        migrations.AddField(
            model_name="delivery",
            name="responding_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="responded_deliveries",
                to="user.Profile",
            ),
        ),
        migrations.AddField(
            model_name="delivery",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="delivery",
                to="projects.Task",
            ),
        ),
    ]
