"use server";

import { cookies } from "next/headers";

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Types
export interface Todo {
  id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface TodoCreateParams {
  title: string;
  description?: string;
}

export interface TodoUpdateParams {
  title?: string;
  description?: string;
  completed?: boolean;
}

// Get authentication token from cookie
async function getAuthToken(): Promise<string | null> {
  const cookieStore = await cookies();
  return cookieStore.get("session")?.value || null;
}

// Make authenticated API request
async function authenticatedFetch(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = await getAuthToken();
  if (!token) {
    throw new Error("Not authenticated");
  }

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...options.headers,
  };

  return fetch(url, {
    ...options,
    headers,
  });
}

// Get all todos
export async function getTodos(): Promise<Todo[]> {
  try {
    const response = await authenticatedFetch(`${API_BASE_URL}/todos`);

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error("Not authenticated");
      }
      throw new Error(`Failed to fetch todos: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching todos:", error);
    throw error;
  }
}

// Get a single todo by ID
export async function getTodo(id: string): Promise<Todo> {
  try {
    const response = await authenticatedFetch(`${API_BASE_URL}/todos/${id}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Todo not found");
      }
      if (response.status === 401) {
        throw new Error("Not authenticated");
      }
      throw new Error(`Failed to fetch todo: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching todo:", error);
    throw error;
  }
}

// Create a new todo
export async function createTodo(params: TodoCreateParams): Promise<Todo> {
  try {
    const response = await authenticatedFetch(`${API_BASE_URL}/todos`, {
      method: "POST",
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      if (response.status === 401) {
        throw new Error("Not authenticated");
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Failed to create todo: ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Error creating todo:", error);
    throw error;
  }
}

// Update a todo
export async function updateTodo(
  id: string,
  params: TodoUpdateParams
): Promise<Todo> {
  try {
    const response = await authenticatedFetch(`${API_BASE_URL}/todos/${id}`, {
      method: "PUT",
      body: JSON.stringify(params),
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Todo not found");
      }
      if (response.status === 401) {
        throw new Error("Not authenticated");
      }
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail || `Failed to update todo: ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Error updating todo:", error);
    throw error;
  }
}

// Delete a todo
export async function deleteTodo(id: string): Promise<void> {
  try {
    const response = await authenticatedFetch(`${API_BASE_URL}/todos/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Todo not found");
      }
      if (response.status === 401) {
        throw new Error("Not authenticated");
      }
      throw new Error(`Failed to delete todo: ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error deleting todo:", error);
    throw error;
  }
}

