<script lang="ts">
  import { goto } from "$app/navigation";
  let email = "";
  let password = "";
  let role = "REPORTER";

  async function handleRegister() {
    const res = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, role }),
    });

    const data = await res.json();

    if (res.ok) {
      alert("Registered successfully!");
      goto("/"); // redirect to login
    } else {
      alert(data.detail || "Registration failed");
    }
  }
</script>

<div class="min-h-screen bg-gray-100 flex items-center justify-center px-4">
  <div class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
    <h2 class="text-3xl font-extrabold text-center text-gray-800 mb-4">Create an Account</h2>
    <p class="text-sm text-gray-500 mb-6 text-center">Sign up to start reporting issues</p>

    <form on:submit|preventDefault={handleRegister} class="space-y-4">
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

      <div>
        <label class="block text-sm font-medium text-gray-700">Role</label>
        <select
          bind:value={role}
          class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="REPORTER">Reporter</option>
          <option value="MAINTAINER">Maintainer</option>
          <option value="ADMIN">Admin</option>
        </select>
      </div>

      <button
        type="submit"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition duration-150"
      >
        Sign Up
      </button>
    </form>
  </div>
</div>
