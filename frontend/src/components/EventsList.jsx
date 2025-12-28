import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../utils/api'

function EventsList({ user }) {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    location: '',
    language: '',
    q: '',
  })
  const navigate = useNavigate()

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (filters.location) params.append('location', filters.location)
      if (filters.language) params.append('language', filters.language)
      if (filters.q) params.append('q', filters.q)

      const response = await api.get(`/events/?${params.toString()}`)
      setEvents(response.data.results || response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load events')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchEvents()
  }

  const handleDelete = async (eventId) => {
    if (!window.confirm('Are you sure you want to delete this event?')) return

    try {
      await api.delete(`/events/${eventId}/`)
      setEvents(events.filter(e => e.id !== eventId))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete event')
    }
  }

  const handleEnroll = async (eventId) => {
    try {
      await api.post('/enrollments/', { event: eventId })
      alert('Successfully enrolled!')
      fetchEvents()
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to enroll'
      alert(errorMsg)
    }
  }

  if (loading) {
    return <div className="loading">Loading events...</div>
  }

  return (
    <div>
      <h1>{user.role === 'Facilitator' ? 'My Events' : 'Browse Events'}</h1>

      {user.role === 'Seeker' && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>Search & Filter</h3>
          <form onSubmit={handleSearch}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Search events..."
                value={filters.q}
                onChange={(e) => setFilters({ ...filters, q: e.target.value })}
              />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div className="form-group">
                <input
                  type="text"
                  placeholder="Location"
                  value={filters.location}
                  onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                />
              </div>
              <div className="form-group">
                <input
                  type="text"
                  placeholder="Language"
                  value={filters.language}
                  onChange={(e) => setFilters({ ...filters, language: e.target.value })}
                />
              </div>
            </div>
            <button type="submit" className="btn btn-primary">Search</button>
          </form>
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {events.length === 0 ? (
        <div className="card">
          <p>No events found.</p>
          {user.role === 'Facilitator' && (
            <Link to="/events/new" className="btn btn-primary">Create Your First Event</Link>
          )}
        </div>
      ) : (
        <div className="grid">
          {events.map(event => (
            <div key={event.id} className="event-card">
              <h3>{event.title}</h3>
              <p>{event.description}</p>
              <div className="meta">
                <div>
                  <p><strong>Location:</strong> {event.location}</p>
                  <p><strong>Language:</strong> {event.language}</p>
                  <p><strong>Starts:</strong> {new Date(event.starts_at).toLocaleString()}</p>
                  {event.capacity && (
                    <p><strong>Available:</strong> {event.available_seats} / {event.capacity}</p>
                  )}
                </div>
              </div>
              <div style={{ marginTop: '15px' }}>
                {user.role === 'Facilitator' ? (
                  <>
                    <Link to={`/events/${event.id}/edit`} className="btn btn-secondary" style={{ marginRight: '10px' }}>
                      Edit
                    </Link>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(event.id)}
                    >
                      Delete
                    </button>
                  </>
                ) : (
                  <button
                    className="btn btn-success"
                    onClick={() => handleEnroll(event.id)}
                    disabled={event.available_seats === 0 || event.is_past}
                  >
                    {event.available_seats === 0 ? 'Full' : event.is_past ? 'Past Event' : 'Enroll'}
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default EventsList

