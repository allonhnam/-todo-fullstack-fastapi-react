import Link from "next/link";
import { Button } from "@/components/ui/button";

const Page = () => {
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
