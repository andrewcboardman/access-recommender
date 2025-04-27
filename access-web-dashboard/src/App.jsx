import React, { useState, useEffect} from 'react';
import { getSuggestions } from "@/lib/api";
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const dummyCredentials = { username: 'user', password: 'password' };

export default function App() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);

  const [supports, setSupports] = useState([]);

  useEffect(() => {
    if (isAuthenticated) {
      getSuggestions({
        name: form.username,
        condition: "Arms or hands",     // <-- dummy for now
        job_role: "Programmers and Software Development Professionals"
      }).then(data => setSupports(data.supports));
    }
  }, [isAuthenticated]);


  const handleLogin = (e) => {
    e.preventDefault();
    if (form.username === dummyCredentials.username && form.password === dummyCredentials.password) {
      setIsAuthenticated(true);
      setError('');
    } else {
      setError('Incorrect username or password');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <Card className="w-full max-w-md shadow-2xl rounded-2xl p-8">
          <h1 className="text-3xl font-bold mb-6 text-gray-900">
            Sign in to your GOV.UK account
          </h1>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="username">
                Username
              </label>
              <Input
                id="username"
                placeholder="user"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="password">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
              />
            </div>
            {error && <p className="text-red-600 text-sm">{error}</p>}
            <Button type="submit" className="w-full text-lg py-2">
              Continue
            </Button>
          </form>
        </Card>
      </div>
    );
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setUploadedFile(file);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-black text-white p-4 flex items-center space-x-2">
        <span className="text-2xl font-bold">GOV.UK</span>
        <span className="sr-only">Dashboard</span>
      </header>

      <main className="flex-grow bg-gray-50 p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* User Info */}
          <Card className="rounded-2xl shadow-md">
            <CardContent className="p-6 space-y-2">
              <h2 className="text-xl font-semibold mb-2">Your details</h2>
              <p><span className="font-medium">Username:</span> {dummyCredentials.username}</p>
              <p><span className="font-medium">Account type:</span> Demo</p>
              <Button onClick={() => setIsAuthenticated(false)} className="mt-4" variant="outline">
                Sign out
              </Button>
            </CardContent>
          </Card>

          {/* Support Suggestions */}
          <Card className="rounded-2xl shadow-md">
            <CardContent className="p-6 space-y-2">
              <h2 className="text-xl font-semibold mb-2">Suggested help</h2>
              <ul className="list-disc list-inside space-y-1">
                {supports.map(s => <li key={s}>{s}</li>)}
              </ul>
              <Button className="mt-4">View more guidance</Button>
            </CardContent>
          </Card>

          {/* Upload Spending */}
          <Card className="rounded-2xl shadow-md">
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">Upload spending</h2>
              <p className="text-sm text-gray-700">
                Upload your recent transactions CSV so we can offer tailored advice.
              </p>
              <Input type="file" accept=".csv" onChange={handleFileChange} />
              {uploadedFile && (
                <p className="text-sm text-gray-800">
                  Selected: {uploadedFile.name}
                </p>
              )}
              <Button disabled={!uploadedFile}>Submit file</Button>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
