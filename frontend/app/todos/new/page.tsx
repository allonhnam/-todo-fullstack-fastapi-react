import { redirect } from "next/navigation";
import { getCurrentUser } from "@/lib/auth.action";
import TodoForm from "@/components/TodoForm";

const NewTodoPage = async () => {
  const user = await getCurrentUser();
  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Create New Todo</h1>
        <TodoForm />
      </div>
    </div>
  );
};

export default NewTodoPage;

