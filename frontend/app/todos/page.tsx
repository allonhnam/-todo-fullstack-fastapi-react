import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getTodos, type Todo } from "@/lib/todo.action";
import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth.action";
import { CheckCircle2, Circle, Plus } from "lucide-react";
import SignOutButton from "@/components/SignOutButton";

const TodosPage = async () => {
  const user = await getCurrentUser();
  if (!user) {
    redirect("/sign-in");
  }

  let todos: Todo[] = [];
  try {
    todos = await getTodos();
  } catch (error) {
    console.error("Error fetching todos:", error);
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold">My Todos</h1>
          <div className="flex gap-4">
            <Button asChild>
              <Link href="/todos/new">
                <Plus className="mr-2 h-4 w-4" />
                New Todo
              </Link>
            </Button>
            <SignOutButton />
          </div>
        </div>

        {todos.length === 0 ? (
          <div className="text-center py-12 border border-dashed rounded-lg">
            <p className="text-muted-foreground text-lg mb-4">
              No todos yet. Create your first todo!
            </p>
            <Button asChild>
              <Link href="/todos/new">Create Todo</Link>
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {todos.map((todo) => (
              <Link
                key={todo.id}
                href={`/todos/${todo.id}`}
                className="block p-6 border rounded-lg hover:bg-accent transition-colors"
              >
                <div className="flex items-start gap-4">
                  <div className="mt-1">
                    {todo.completed ? (
                      <CheckCircle2 className="h-5 w-5 text-green-500" />
                    ) : (
                      <Circle className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h2
                      className={`text-xl font-semibold mb-2 ${
                        todo.completed ? "line-through text-muted-foreground" : ""
                      }`}
                    >
                      {todo.title}
                    </h2>
                    {todo.description && (
                      <p
                        className={`text-muted-foreground ${
                          todo.completed ? "line-through" : ""
                        }`}
                      >
                        {todo.description}
                      </p>
                    )}
                    <div className="mt-2 text-sm text-muted-foreground">
                      {todo.created_at &&
                        new Date(todo.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TodosPage;

