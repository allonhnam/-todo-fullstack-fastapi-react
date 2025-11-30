"use client";

import { z } from "zod";
import Link from "next/link";
import { toast } from "sonner";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";

import { Form } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { signIn, signUp } from "@/lib/auth.action";
import FormField from "./FormField";

type FormType = "sign-in" | "sign-up";

const authFormSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  password: z.string().min(3, "Password must be at least 3 characters"),
});

const AuthForm = ({ type }: { type: FormType }) => {
  const router = useRouter();

  const form = useForm<z.infer<typeof authFormSchema>>({
    resolver: zodResolver(authFormSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit = async (data: z.infer<typeof authFormSchema>) => {
    try {
      if (type === "sign-up") {
        const { username, password } = data;

        const result = await signUp({
          username,
          password,
        });

        if (!result?.success) {
          toast.error(result?.message || "Failed to create account");
          return;
        }

        toast.success(result.message || "Account created successfully. Please sign in.");
        router.push("/sign-in");
      } else {
        const { username, password } = data;

        const result = await signIn({
          username,
          password,
        });

        if (!result?.success) {
          toast.error(result?.message || "Failed to sign in");
          return;
        }

        toast.success(result.message || "Signed in successfully.");
        router.push("/todos");
      }
    } catch (error) {
      console.error("Auth error:", error);
      toast.error(`There was an error: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  };

  const isSignIn = type === "sign-in";

  return (
    <div className="max-w-md mx-auto mt-8 p-6 border border-gray-300 rounded-lg shadow-md">
      <div className="flex flex-col gap-6">
        <div className="flex flex-row gap-2 justify-center">
          <h2 className="text-2xl font-bold text-blue-600">Todo App</h2>
        </div>

        <h3 className="text-xl font-semibold text-center">Welcome Back</h3>

        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(onSubmit)}
            className="w-full space-y-6 mt-4"
          >
            <FormField
              control={form.control}
              name="username"
              label=""
              placeholder="Username"
              type="text"
            />

            <FormField
              control={form.control}
              name="password"
              label=""
              placeholder="Password"
              type="password"
            />

            <Button className="w-full" type="submit">
              {isSignIn ? "Sign In" : "Create an Account"}
            </Button>
          </form>
        </Form>

        <p className="text-center text-sm">
          {isSignIn ? "No account yet?" : "Have an account already?"}
          <Link
            href={!isSignIn ? "/sign-in" : "/sign-up"}
            className="font-bold text-blue-600 ml-1 hover:underline"
          >
            {!isSignIn ? "Sign In" : "Sign Up"}
          </Link>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;
