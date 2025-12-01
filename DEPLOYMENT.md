# Vercel Deployment Guide

## Configuration

This project has a monorepo structure with the Next.js frontend in the `frontend` directory.

### Required: Configure Root Directory in Vercel Dashboard

Since `rootDirectory` is not a valid property in `vercel.json`, you **must** configure it in the Vercel dashboard:

1. Go to your project settings in Vercel
2. Navigate to **Settings** → **General**
3. Under **Root Directory**, click **Edit**
4. Set the root directory to: `frontend`
5. Click **Save**

Vercel will automatically:
- Detect Next.js framework
- Use default build commands (`npm run build`)
- Set the correct output directory (`.next`)

**Note**: The root directory setting is project-wide and applies to all deployments.

## Required Environment Variables

Make sure to set these environment variables in your Vercel project settings:

```
NEXT_PUBLIC_API_URL=https://your-backend-api-url.com
```

If your backend is also deployed, use that URL. For local development, it's `http://localhost:8000`.

## Backend Deployment

The backend (FastAPI) needs to be deployed separately. Options:
- Deploy to a service like Railway, Render, or AWS
- Use Vercel Serverless Functions (requires adaptation)
- Deploy to a VPS or cloud instance

### Backend CORS Configuration

The backend CORS has been updated to accept origins from environment variables. When deploying your backend:

1. Set the `ALLOWED_ORIGINS` environment variable with your Vercel domain(s):
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,https://your-custom-domain.com
   ```

2. The backend will automatically allow:
   - `http://localhost:3000` (local development)
   - `http://localhost:8000` (local backend)
   - Any domains you add to `ALLOWED_ORIGINS`

3. **Important**: Add your Vercel preview and production domains to `ALLOWED_ORIGINS`

## Troubleshooting

### 404 NOT_FOUND Error

**This is the most common issue!** If you're getting a 404 error on your Vercel deployment:

1. **CRITICAL: Set Root Directory in Vercel Dashboard**
   - Go to your Vercel project → **Settings** → **General**
   - Scroll to **Root Directory**
   - Click **Edit** and set it to: `frontend`
   - Click **Save**
   - **Redeploy** your project (push a new commit or redeploy from dashboard)

2. **Check Build Logs**: Look for any build errors in the Vercel deployment logs
   - If you see "Cannot find module" or similar errors, the root directory is likely wrong

3. **Verify Routes**: Ensure all route files exist:
   - `app/page.tsx` (home page)
   - `app/todos/page.tsx` (todos list)
   - `app/todos/new/page.tsx` (new todo)
   - `app/todos/[id]/page.tsx` (todo detail)
   - `app/(auth)/sign-in/page.tsx` (sign in)
   - `app/(auth)/sign-up/page.tsx` (sign up)

### Build Errors

- Check that all dependencies are in `package.json`
- Ensure Node.js version is compatible (check `package.json` engines if specified)
- Review build logs for specific error messages

### Environment Variables

- Make sure `NEXT_PUBLIC_API_URL` is set correctly
- Environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Other variables are only available in server-side code

