<script lang="ts">
  import "../app.css";
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  /* ─── Auth presence ─────────────────────────────────── */
  let isAuthenticated = false;
  onMount(() => {
    isAuthenticated = !!localStorage.getItem('token');
  });
  function logout() {
    localStorage.removeItem('token');
    goto('/');
  }

  /* ─── Dark-mode toggle ──────────────────────────────── */
  let dark = false;
  onMount(() => {
    dark = localStorage.getItem('theme') === 'dark';
    applyTheme();
  });
  function toggleTheme() {
    dark = !dark;
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    applyTheme();
  }
  function applyTheme() {
    if (dark) document.documentElement.classList.add('dark');
    else      document.documentElement.classList.remove('dark');
  }
</script>

{#if isAuthenticated}
  <div class="min-h-screen flex bg-gray-100 dark:bg-gray-900">
    <!-- Sidebar -->
    <aside class="w-64 bg-white dark:bg-gray-800 shadow-lg hidden md:block">
      <div class="p-4 font-bold text-xl border-b dark:border-gray-700 dark:text-gray-100">Tracker</div>
      <nav class="p-4 space-y-2 text-sm">
        <a href="/dashboard" class="block text-gray-700 dark:text-gray-300 hover:text-blue-600">Dashboard</a>
        <a href="/issues"    class="block text-gray-700 dark:text-gray-300 hover:text-blue-600">Issues</a>
        <a href="/submit"    class="block text-gray-700 dark:text-gray-300 hover:text-blue-600">Submit New</a>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1">
      <header class="flex items-center justify-between bg-white dark:bg-gray-800 shadow px-6 py-4">
        <h1 class="text-xl font-semibold text-gray-800 dark:text-gray-100">
          Issues & Insights
        </h1>

        <div class="flex items-center gap-4">
          <!-- ☀️ / 🌙 toggle -->
          <button
            on:click={toggleTheme}
            class="text-xl focus:outline-none text-gray-600 dark:text-gray-300"
            title="Toggle dark mode">
            {#if dark} 🌙 {:else} ☀️ {/if}
          </button>

          <button
            on:click={logout}
            class="text-sm bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-100 px-4 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-600">
            Logout
          </button>
        </div>
      </header>

      <div class="p-6">
        <slot />
      </div>
    </main>
  </div>
{:else}
  <!-- Unauthenticated routes (login/register) -->
  <slot />
{/if}
