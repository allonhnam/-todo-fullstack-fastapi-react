"use client";

import { z } from "zod";
import { toast } from "sonner";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";

import { Form } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { createTodo, updateTodo, type Todo } from "@/lib/todo.action";
import FormField from "./FormField";

const todoFormSchema = z.object({
  title: z.string().min(1, "Title is required"),
  description: z.string().optional(),
});

interface TodoFormProps {
  todo?: Todo;
  mode?: "create" | "edit";
}

const TodoForm = ({ todo, mode = "create" }: TodoFormProps) => {
  const router = useRouter();

  const form = useForm<z.infer<typeof todoFormSchema>>({
    resolver: zodResolver(todoFormSchema),
    defaultValues: {
      title: todo?.title || "",
      description: todo?.description || "",
    },
  });

  const onSubmit = async (data: z.infer<typeof todoFormSchema>) => {
    try {
      if (mode === "create") {
        await createTodo({
          title: data.title,
          description: data.description || undefined,
        });
        toast.success("Todo created successfully");
        router.push("/todos");
      } else if (todo) {
        await updateTodo(todo.id, {
          title: data.title,
          description: data.description || undefined,
        });
        toast.success("Todo updated successfully");
        router.push("/todos");
      }
    } catch (error) {
      console.error("Todo error:", error);
      toast.error(
        `There was an error: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  };

  return (
    <div className="border rounded-lg p-6 shadow-md">
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="w-full space-y-6"
        >
          <FormField
            control={form.control}
            name="title"
            label="Title"
            placeholder="Enter todo title"
            type="text"
          />

          <div className="space-y-2">
            <label htmlFor="description" className="block text-sm font-medium">
              Description
            </label>
            <textarea
              {...form.register("description")}
              id="description"
              placeholder="Enter todo description (optional)"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[100px]"
            />
          </div>

          <div className="flex gap-4">
            <Button type="submit">
              {mode === "create" ? "Create Todo" : "Update Todo"}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => router.push("/todos")}
            >
              Cancel
            </Button>
          </div>
        </form>
      </Form>
    </div>
  );
};

export default TodoForm;

