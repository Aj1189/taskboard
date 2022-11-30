import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {HttpClient} from '@angular/common/http';

type Status = 'todo' | 'doing' | 'done' | 'rejected';

interface Task {
  title: string;
  description: string;
  status: Status;
}

@Injectable({
  providedIn: 'root'
})
export class TaskService {

  constructor(private http: HttpClient) {
  }

  public getAll(): Observable<Task[]> {
    return this.http.get<Task[]>('/api/tasks');
  }

  public deleteOne(id): Observable<any> {
    return this.http.delete<{ status: string }>(`/api/tasks/${id}`);
  }

  public updateOne(id, title, description): Observable<any> {
    return this.http.put<{ status: string }>(`/api/tasks/${id}`, {
      title, description
    });
  }

  public move(id, toStatus, toPosition) {
    return this.http.put(`/api/tasks/${id}`, {status: toStatus, after: toPosition});
  }

  public createOne(title, description): Observable<any> {
    return this.http.post<{ status: string }>(`/api/tasks`, {
      title, description, status: 'todo'
    });
  }
}
