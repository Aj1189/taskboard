import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {MatDialog} from '@angular/material/dialog';
import {
  CdkDragDrop,
  moveItemInArray,
  transferArrayItem,
} from '@angular/cdk/drag-drop';
import {FormControl, FormGroup} from '@angular/forms';
import {TaskService} from '../services/task.service';
import {Task} from 'protractor/built/taskScheduler';

@Component({
  selector: 'tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css']
})
export class TasksComponent implements OnInit {

  @ViewChild('closeModalButton') closeModalButton: ElementRef;

  newTaskForm: FormGroup;

  todo = [];
  doing = [];
  done = [];
  rejected = [];

  constructor(public dialog: MatDialog, private task: TaskService) {
  }


  ngOnInit() {
    this.reload();


    this.newTaskForm = new FormGroup({
      title: new FormControl(null),
      description: new FormControl(null),
      id: new FormControl(null)
    });
  }

  reload() {
    this.task.getAll().subscribe(res => {
      if (res) {
        console.log(res);
        this.todo = res.filter(t => !t.status || t.status === 'todo');
        this.doing = res.filter(t => t.status === 'doing');
        this.done = res.filter(t => t.status === 'done');
        this.rejected = res.filter(t => t.status === 'rejected');
      }
    });
  }

  addTask() {
    const task = this.newTaskForm.value;
    if (task.id) {
      this.task.updateOne(task.id, task.title, task.description).subscribe(res => {
        this.reload();
        this.closeModalButton.nativeElement.click();
      });
    } else {
      this.task.createOne(task.title, task.description).subscribe(res => {
        this.reload();
      });
    }

    this.newTaskForm.reset();
  }

  drop(event: CdkDragDrop<any>, droppedStatus: string) {

    if (event.previousContainer === event.container) {
      moveItemInArray(
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }

    const movedTask = event.container.data[event.currentIndex];
    this.task.move(movedTask.id, droppedStatus, event.currentIndex).subscribe(result => {
      this.reload();
    });
  }


  deleteTask(tasksToDelete) {
    this.task.deleteOne(tasksToDelete.id).subscribe(res => {
      this.reload();
    });
  }

  editTask(task) {
    this.newTaskForm.patchValue(task);

  }
}
