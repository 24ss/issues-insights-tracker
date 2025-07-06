<script lang="ts">
  import { onMount } from 'svelte';

  // ── Email / password login ───────────────────────────
  let email = '';
  let password = '';

  async function handleLogin() {
    const res = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.access_token);
      location.href = '/';      // redirect to app
    } else alert(data.detail || 'Login failed');
  }

  // ── Google OAuth login ───────────────────────────────
  const GOOGLE_CLIENT_ID = '113059113270-imssn8ht2572ht5d5imcn49sciesbhu1.apps.googleusercontent.com'; // <-- replace

  onMount(() => {
    // Load Google script once
    const s = document.createElement('script');
    s.src = 'https://accounts.google.com/gsi/client';
    s.onload = () => {
      // @ts-ignore
      google.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: handleGoogle
      });
      // @ts-ignore
      google.accounts.id.renderButton(
        document.getElementById('g-btn'),
        { theme: 'outline', size: 'large', width: '240' }
      );
    };
    document.head.appendChild(s);
  });

  async function handleGoogle(resp: any) {
    const res = await fetch('http://localhost:8000/api/auth/google-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_token: resp.credential })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.access_token);
      location.href = '/';
    } else alert('Google login failed');
  }
</script>

<div class="min-h-screen bg-gray-100 flex items-center justify-center px-4">
  <div class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
    <h2 class="text-3xl font-extrabold text-center text-gray-800 mb-4">
      Welcome Back
    </h2>
    <p class="text-sm text-gray-500 mb-6 text-center">
      Sign in to your account
    </p>

    <!-- email / password form -->
    <form on:submit|preventDefault={handleLogin} class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          type="email"
          bind:value={email}
          required
          class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input
          type="password"
          bind:value={password}
          required
          class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition duration-150"
      >
        Sign In
      </button>
    </form>

    <!-- Google button placeholder -->
    <div id="g-btn" class="flex justify-center mt-6"></div>
  </div>
</div>
