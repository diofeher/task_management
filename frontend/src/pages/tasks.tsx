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

  return (
    <TaskProvider>
      <TaskInput addTask={addTask} />
      <ul>
      {tasks.map((task: Task) => (
          <li key={task.id} style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
          <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTaskCompletion(task.id)}
          />
          <span>{task.title} - {task.description}</span>
          <button onClick={() => deleteTask(task.id)}>Delete</button>
          <button onClick={() => {
              const newText = prompt('Edit task:', task.text);
              if (newText) updateTask(task.id, newText);
          }}>Edit</button>
          </li>
      ))}
      </ul>
    </TaskProvider>
  );
};

export default TaskList;
