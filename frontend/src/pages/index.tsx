import React, { useEffect } from 'react';
import { Task, useTaskContext } from '../contexts/TaskContext';

import TaskInput from '@/components/TaskInput';
import { TaskProvider } from '../contexts/TaskContext';
import { useAuth } from '../contexts/AuthContext';

const TaskList: React.FC = () => {
  const { tasks, updateTask, deleteTask, addTask, fetchTasks, toggleTaskCompletion } = useTaskContext();
  const { user } = useAuth();

  useEffect(() => {
    if(user) {
      fetchTasks();
    }
  }, [user]);

  if(!user) {
    return false;
  }

  const onEdit = (task: Task) => () => {
      const newText = prompt('Edit task:', task.title);
      if (newText) updateTask(task.id, newText);
  }

  const readableDate = (dt: string) => {
    return new Date(dt).toLocaleDateString('default', { day: 'numeric', month: 'short' });
  }

  const onDelete = (id: number) => () => deleteTask(id);
  const onCompleted = (id: number) => () => toggleTaskCompletion(id);

  return (
    <TaskProvider>
      <div className="block">
        <h1>Task list</h1>
        <ul className="task-list">
        {tasks.map((task: Task) => (
            <li key={task.id} style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
            <div className="checkbox-container">
              <input
                readOnly
                type="checkbox"
                className="rounded-checkbox"
                checked={task.completed}
              />
              <span onClick={onCompleted(task.id)} className="custom-checkbox"></span>
            </div>
            <div className="information">
              <span className="title">{task.title}</span>
              <span className="description">{task.description}</span>
            </div>
            <div className="action-buttons">
              <span className="date">{readableDate(task.due_date)}</span>
              <button onClick={onEdit(task)}>Edit</button>
              <button className="delete" onClick={onDelete(task.id)}>X</button>
            </div>
            <div style={{clear: "both"}}></div>
            </li>
        ))}
        </ul>
        <TaskInput addTask={addTask} />
      </div>
    </TaskProvider>
  );
};

export default TaskList;
