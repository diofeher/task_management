"use client";

import { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import { apiFetch, authHeader } from "../utils/api";

import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';

export type Task = {
  id: number;
  title: string;
  description: string;
  dueDate: string; // ISO date format (string)
  completed: boolean;
};

type TaskContextType = {
  tasks: Task[];
  addTask: (title: string, description: string, dueDate: string) => Promise<void>;
  updateTask: (id: number, newText: string) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
  toggleTaskCompletion: (id: number) => Promise<void>;
  fetchTasks: () => Promise<void>;
};

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const { user } = useAuth();
  console.log("TaskProvider", user);
  
  // Fetch all tasks from the API
  const fetchTasks = async () => {
    try {
      const response = await apiFetch('/tasks/', {
        headers: authHeader(user),
      });
      const data = await response;
      setTasks(data);
    } catch (e) {
      toast.error(e.toString());
    }
  };

  // Add a new task via the API
  const addTask = async (title: string, description: string, dueDate: string) => {
    try {
      const newTask = await apiFetch('/tasks', {
        method: 'POST',
        headers: authHeader(user),
        body: { title, description, due_date: dueDate, completed: false }
      });
      console.log("added Task", newTask);
      // setTasks((prevTasks) => {
      //   console.log("OK!!", prevTasks, newTask);
      //   return [...prevTasks, newTask]
      // });
      // setTasks((prevTasks) => {
      //   // [...prevTasks, {title: title}]);
      //   return [{title: 1, description: 1}];
      // });
      setTasks([]);
    } catch (error) {
      console.error("Failed to add task:", error);
    }
  };

  // Update a task via the API
  const updateTask = async (id: number, newText: string) => {
    try {
      await apiFetch(`/tasks/${id}`, {
        method: 'PATCH',
        headers: authHeader(user),
        body: { title: newText }
      });
      setTasks((prevTasks) => prevTasks.map((task) => task.id === id ? { ...task, title: newText } : task));
    } catch (error) {
      console.error("Failed to update task:", error);
    }
  };

  // Delete a task via the API
  const deleteTask = async (id: number) => {
    try {
      await apiFetch(`/tasks/${id}`, {
        method: 'DELETE',
        headers: authHeader(user)
      });
      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== id));
    } catch (error) {
      console.error("Failed to delete task:", error);
    }
  };

  // Toggle task completion status via the API
  const toggleTaskCompletion = async (id: number) => {
    try {
      const task = tasks.find((task) => task.id === id);
      if (task) {
        await apiFetch(`/tasks/${id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed: !task.completed })
        });
        setTasks((prevTasks) =>
          prevTasks.map((task) =>
            task.id === id ? { ...task, completed: !task.completed } : task
          )
        );
      }
    } catch (error) {
      console.error("Failed to toggle task completion:", error);
    }
  };

  return (
    <TaskContext.Provider value={{ user, tasks, addTask, updateTask, deleteTask, toggleTaskCompletion, fetchTasks }}>
      {children}
    </TaskContext.Provider>
  );
};

export const useTaskContext = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};
