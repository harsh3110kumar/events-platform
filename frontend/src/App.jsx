import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './components/Login'
import Signup from './components/Signup'
import VerifyEmail from './components/VerifyEmail'
import Dashboard from './components/Dashboard'
import EventsList from './components/EventsList'
import EventForm from './components/EventForm'
import MyEnrollments from './components/MyEnrollments'
import Navbar from './components/Navbar'
import { getToken, removeToken } from './utils/auth'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (token) {
      // Fetch user profile
      fetch('http://localhost:8000/api/auth/profile/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (res.ok) {
            return res.json()
          }
          removeToken()
          return null
        })
        .then(data => {
          if (data) {
            setUser(data)
          }
          setLoading(false)
        })
        .catch(() => {
          removeToken()
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }, [])

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <Router>
      <div className="App">
        {user && <Navbar user={user} onLogout={() => { removeToken(); setUser(null) }} />}
        <div className="container">
          <Routes>
            <Route path="/login" element={!user ? <Login onLogin={setUser} /> : <Navigate to="/" />} />
            <Route path="/signup" element={!user ? <Signup /> : <Navigate to="/" />} />
            <Route path="/verify-email" element={!user ? <VerifyEmail /> : <Navigate to="/" />} />
            <Route path="/" element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} />
            <Route path="/events" element={user ? <EventsList user={user} /> : <Navigate to="/login" />} />
            <Route path="/events/new" element={user?.role === 'Facilitator' ? <EventForm /> : <Navigate to="/" />} />
            <Route path="/events/:id/edit" element={user?.role === 'Facilitator' ? <EventForm /> : <Navigate to="/" />} />
            <Route path="/my-enrollments" element={user?.role === 'Seeker' ? <MyEnrollments /> : <Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App

