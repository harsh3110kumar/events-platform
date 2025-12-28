import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import api from '../utils/api'

function EventForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    language: '',
    location: '',
    starts_at: '',
    ends_at: '',
    capacity: '',
  })

  useEffect(() => {
    if (id) {
      fetchEvent()
    }
  }, [id])

  const fetchEvent = async () => {
    try {
      const response = await api.get(`/events/${id}/`)
      const event = response.data
      setFormData({
        title: event.title,
        description: event.description,
        language: event.language,
        location: event.location,
        starts_at: event.starts_at.slice(0, 16), // Format for datetime-local
        ends_at: event.ends_at.slice(0, 16),
        capacity: event.capacity || '',
      })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load event')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const data = {
        ...formData,
        capacity: formData.capacity ? parseInt(formData.capacity) : null,
        starts_at: new Date(formData.starts_at).toISOString(),
        ends_at: new Date(formData.ends_at).toISOString(),
      }

      if (id) {
        await api.put(`/events/${id}/`, data)
      } else {
        await api.post('/events/', data)
      }
      navigate('/events')
    } catch (err) {
      const errorData = err.response?.data
      if (typeof errorData === 'object') {
        const errors = Object.values(errorData).flat()
        setError(errors.join(', '))
      } else {
        setError(errorData?.detail || 'Failed to save event')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="card" style={{ maxWidth: '600px', margin: '20px auto' }}>
      <h2>{id ? 'Edit Event' : 'Create New Event'}</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Description *</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
            rows="5"
          />
        </div>
        <div className="form-group">
          <label>Language *</label>
          <input
            type="text"
            name="language"
            value={formData.language}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Location *</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Starts At (UTC) *</label>
          <input
            type="datetime-local"
            name="starts_at"
            value={formData.starts_at}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Ends At (UTC) *</label>
          <input
            type="datetime-local"
            name="ends_at"
            value={formData.ends_at}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Capacity (optional)</label>
          <input
            type="number"
            name="capacity"
            value={formData.capacity}
            onChange={handleChange}
            min="1"
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Saving...' : id ? 'Update Event' : 'Create Event'}
        </button>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => navigate('/events')}
          style={{ marginLeft: '10px' }}
        >
          Cancel
        </button>
      </form>
    </div>
  )
}

export default EventForm

