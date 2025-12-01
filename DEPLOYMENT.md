# Vercel Deployment Guide

## Configuration

This project has a monorepo structure with the Next.js frontend in the `frontend` directory.

### ⚠️ CRITICAL: Configure Root Directory in Vercel Dashboard

**This is REQUIRED for your deployment to work!** Since your Next.js app is in the `frontend` subdirectory, you **must** set the root directory in Vercel:

1. Go to your Vercel project dashboard
2. Click on **Settings** (gear icon)
3. Go to **General** tab
4. Scroll down to **Root Directory**
5. Click **Edit**
6. Enter: `frontend`
7. Click **Save**

**After saving, you MUST redeploy:**
- Either push a new commit to trigger a new deployment
- Or go to **Deployments** tab and click **Redeploy** on the latest deployment

Vercel will then:
- ✅ Detect Next.js framework automatically
- ✅ Run `npm install` in the `frontend` directory
- ✅ Run `npm run build` in the `frontend` directory  
- ✅ Use `.next` as the output directory (Next.js default)
- ✅ Handle all routing automatically (Next.js App Router)

**Why this is needed:** Vercel looks for `package.json` and `next.config.ts` in the root by default. Since yours are in `frontend/`, Vercel can't find your Next.js app without this setting.

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

