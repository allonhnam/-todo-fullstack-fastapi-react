"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { deleteTodo, updateTodo, type Todo } from "@/lib/todo.action";
import TodoForm from "./TodoForm";
import { Trash2, Edit, CheckCircle2, Circle, ArrowLeft } from "lucide-react";

interface TodoDetailProps {
  todo: Todo;
}

const TodoDetail = ({ todo: initialTodo }: TodoDetailProps) => {
  const router = useRouter();
  const [todo, setTodo] = useState(initialTodo);
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggleComplete = async () => {
    try {
      const updatedTodo = await updateTodo(todo.id, {
        completed: !todo.completed,
      });
      setTodo(updatedTodo);
      toast.success(
        updatedTodo.completed
          ? "Todo marked as complete"
          : "Todo marked as incomplete"
      );
    } catch (error) {
      console.error("Error updating todo:", error);
      toast.error(
        `Failed to update todo: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  };

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this todo?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTodo(todo.id);
      toast.success("Todo deleted successfully");
      router.push("/todos");
    } catch (error) {
      console.error("Error deleting todo:", error);
      toast.error(
        `Failed to delete todo: ${error instanceof Error ? error.message : "Unknown error"}`
      );
      setIsDeleting(false);
    }
  };

  if (isEditing) {
    return (
      <div className="min-h-screen p-8">
        <div className="max-w-2xl mx-auto">
          <Button
            variant="ghost"
            onClick={() => setIsEditing(false)}
            className="mb-4"
          >
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
          <h1 className="text-4xl font-bold mb-8">Edit Todo</h1>
          <TodoForm todo={todo} mode="edit" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <Button asChild variant="ghost" className="mb-4">
          <Link href="/todos">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Todos
          </Link>
        </Button>

        <div className="border rounded-lg p-6 shadow-md">
          <div className="flex items-start gap-4 mb-6">
            <button
              onClick={handleToggleComplete}
              className="mt-1 hover:opacity-80 transition-opacity"
            >
              {todo.completed ? (
                <CheckCircle2 className="h-6 w-6 text-green-500" />
              ) : (
                <Circle className="h-6 w-6 text-gray-400" />
              )}
            </button>
            <div className="flex-1">
              <h1
                className={`text-3xl font-bold mb-2 ${
                  todo.completed
                    ? "line-through text-muted-foreground"
                    : ""
                }`}
              >
                {todo.title}
              </h1>
              {todo.description && (
                <p
                  className={`text-lg text-muted-foreground mb-4 ${
                    todo.completed ? "line-through" : ""
                  }`}
                >
                  {todo.description}
                </p>
              )}
              <div className="text-sm text-muted-foreground space-y-1">
                {todo.created_at && (
                  <div>
                    Created: {new Date(todo.created_at).toLocaleString()}
                  </div>
                )}
                {todo.updated_at && (
                  <div>
                    Updated: {new Date(todo.updated_at).toLocaleString()}
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="flex gap-4 pt-4 border-t">
            <Button onClick={() => setIsEditing(true)} variant="outline">
              <Edit className="mr-2 h-4 w-4" />
              Edit
            </Button>
            <Button
              onClick={handleDelete}
              variant="destructive"
              disabled={isDeleting}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              {isDeleting ? "Deleting..." : "Delete"}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TodoDetail;

