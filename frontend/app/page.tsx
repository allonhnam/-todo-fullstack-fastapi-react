import Link from "next/link";
import { Button } from "@/components/ui/button";
import { getCurrentUser } from "@/lib/auth.action";
import SignOutButton from "@/components/SignOutButton";

const Page = async () => {
  const user = await getCurrentUser();

  if (user) {
    // User is logged in - show welcome message and sign out button
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-8 p-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">Welcome back, {user.username}!</h1>
          <p className="text-muted-foreground text-lg">
            You are successfully logged in to Todo App
          </p>
        </div>

        <div className="flex gap-4">
          <SignOutButton />
        </div>
      </div>
    );
  }

  // User is not logged in - show sign in/sign up buttons
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-8 p-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">Welcome to Todo App</h1>
        <p className="text-muted-foreground text-lg">
          Manage your tasks efficiently and stay organized
        </p>
      </div>

      <div className="flex gap-4">
        <Button asChild size="lg">
          <Link href="/sign-in">Sign In</Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link href="/sign-up">Sign Up</Link>
        </Button>
      </div>
    </div>
  );
};

export default Page;
