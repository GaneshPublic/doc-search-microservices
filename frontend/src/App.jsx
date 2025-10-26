import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'

// Use environment variable or fallback to service name / localhost
// Use relative path for backend API
const API_BASE = '/api'; // instead of 'http://docsearch-backend:8000'
console.log('API_BASE set to:', API_BASE);

console.log('API_BASE set to:', API_BASE)

function App() {
    const [q, setQ] = useState('')
    const [results, setResults] = useState([])
    const [title, setTitle] = useState('')
    const [body, setBody] = useState('')

    async function doSearch(e) {
        e && e.preventDefault()
        console.log('Searching for:', q)
        try {
            const url = `${API_BASE}/search?q=${encodeURIComponent(q)}`
            console.log('Fetch URL:', url)
            const res = await fetch(url)
            if (!res.ok) throw new Error(`Search failed: ${res.statusText}`)
            const j = await res.json()
            console.log('Search results:', j)
            setResults(j)
        } catch (err) {
            console.error('Error in doSearch:', err)
            alert('Search failed. Check console.')
        }
    }

    async function addDoc(e) {
        e && e.preventDefault()
        console.log('Adding document:', { title, body })
        try {
            const url = `${API_BASE}/documents`
            console.log('POST URL:', url)
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, body }),
            })
            if (!res.ok) throw new Error(`Add document failed: ${res.statusText}`)
            const j = await res.json()
            console.log('Added document response:', j)
            setTitle('')
            setBody('')
            setResults([j, ...results])
        } catch (err) {
            console.error('Error in addDoc:', err)
            alert('Failed to add document. Check console.')
        }
    }

    return (
        <div style={{ padding: 20, fontFamily: 'Arial' }}>
            <h1>Document Search (MongoDB)</h1>

            <form onSubmit={addDoc} style={{ marginBottom: 20 }}>
                <h3>Add document</h3>
                <input
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <br />
                <textarea
                    placeholder="Body"
                    value={body}
                    onChange={(e) => setBody(e.target.value)}
                />
                <br />
                <button type="submit">Add</button>
            </form>

            <form onSubmit={doSearch}>
                <input
                    placeholder="Search..."
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                />
                <button type="submit">Search</button>
            </form>

            <ul>
                {results.map((r) => (
                    <li key={r.id}>
                        <strong>{r.title}</strong>
                        <p>{r.body}</p>
                    </li>
                ))}
            </ul>
        </div>
    )
}

createRoot(document.getElementById('root')).render(<App />)
export default App