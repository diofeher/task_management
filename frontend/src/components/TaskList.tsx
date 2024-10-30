"use client";

import { Task, useTaskContext } from '../contexts/TaskContext';

const TaskList = () => {
  const { tasks, updateTask, deleteTask, toggleTaskCompletion } = useTaskContext();

  return (
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
  );
};

export default TaskList;
