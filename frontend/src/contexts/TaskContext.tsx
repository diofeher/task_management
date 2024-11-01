"use client";

import { ReactNode, createContext, useContext, useEffect, useState } from 'react';
import { apiFetch, authHeader } from "../utils/api";

import { isRedirectError } from "next/dist/client/components/redirect";
import toast from 'react-hot-toast';
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'next/router';

export type Task = {
  id: number;
  title: string;
  description: string;
  due_date: string; // ISO date format (string)
  status: string;
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

const calculateStatus = (status: string) => {
  if(status == "created") {
    return "finished";
  }
  else {
    return "created";
  }

}

const TaskContext = createContext<TaskContextType | undefined>(undefined);

const redirectToLogin = (status, router) => {
  if(status == 401) {
    router.push("/login");
  }
}

export const TaskProvider = ({ children }: { children: ReactNode }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const { user } = useAuth();
  const router = useRouter()
  
  // Fetch all tasks from the API
  const fetchTasks = async () => {
    let response;
    try {
      response = await apiFetch('/tasks/', {
        headers: authHeader(user),
      });
      
      console.log("response.status", response.status);
      redirectToLogin(response.status, router);
      const data = (await response.json()).map((obj: Task) => ({ ...obj, completed: obj.status == "finished" }))
      setTasks(data);
    } catch (error) {
      toast.error(error.toString());
    }
  };

  // Add a new task via the API
  const addTask = async (title: string, description: string, dueDate: string) => {
    try {
      const response = await apiFetch('/tasks', {
        method: 'POST',
        headers: authHeader(user),
        body: { title, description, due_date: dueDate, completed: false }
      });
      const newTask = await response.json();
      setTasks((prevTasks) => [...prevTasks, newTask]);
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
        const newTask: Task = await(await apiFetch(`/tasks/${task.id}`, {
          method: 'PATCH',
          headers: authHeader(user),
          body: { status: calculateStatus(task.status) }
        })).json();

        setTasks((prevTasks) =>
          prevTasks.map((task) => newTask.id === task.id ? {...newTask, completed: newTask.status == "finished" } : task));
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
