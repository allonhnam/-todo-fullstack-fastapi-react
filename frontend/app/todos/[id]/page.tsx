import { redirect, notFound } from "next/navigation";
import { getCurrentUser } from "@/lib/auth.action";
import { getTodo, deleteTodo } from "@/lib/todo.action";
import TodoDetail from "@/components/TodoDetail";

interface TodoPageProps {
  params: Promise<{ id: string }>;
}

const TodoPage = async ({ params }: TodoPageProps) => {
  const user = await getCurrentUser();
  if (!user) {
    redirect("/sign-in");
  }

  const { id } = await params;

  let todo;
  try {
    todo = await getTodo(id);
  } catch (error) {
    console.error("Error fetching todo:", error);
    notFound();
  }

  return <TodoDetail todo={todo} />;
};

export default TodoPage;

