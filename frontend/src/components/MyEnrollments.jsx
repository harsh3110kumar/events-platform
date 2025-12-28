import { useState, useEffect } from 'react'
import api from '../utils/api'

function MyEnrollments() {
  const [enrollments, setEnrollments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('upcoming')

  useEffect(() => {
    fetchEnrollments()
  }, [activeTab])

  const fetchEnrollments = async () => {
    try {
      setLoading(true)
      let response
      if (activeTab === 'upcoming') {
        response = await api.get('/enrollments/upcoming/')
      } else {
        response = await api.get('/enrollments/past/')
      }
      setEnrollments(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load enrollments')
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (enrollmentId) => {
    if (!window.confirm('Are you sure you want to cancel this enrollment?')) return

    try {
      await api.patch(`/enrollments/${enrollmentId}/`, { status: 'canceled' })
      setEnrollments(enrollments.filter(e => e.id !== enrollmentId))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to cancel enrollment')
    }
  }

  if (loading) {
    return <div className="loading">Loading enrollments...</div>
  }

  return (
    <div>
      <h1>My Enrollments</h1>

      <div style={{ marginBottom: '20px' }}>
        <button
          className={`btn ${activeTab === 'upcoming' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('upcoming')}
          style={{ marginRight: '10px' }}
        >
          Upcoming
        </button>
        <button
          className={`btn ${activeTab === 'past' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => setActiveTab('past')}
        >
          Past
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {enrollments.length === 0 ? (
        <div className="card">
          <p>No {activeTab} enrollments found.</p>
        </div>
      ) : (
        <div className="grid">
          {enrollments.map(enrollment => (
            <div key={enrollment.id} className="event-card">
              <h3>{enrollment.event_title}</h3>
              <p><strong>Location:</strong> {enrollment.event_location}</p>
              <p><strong>Starts:</strong> {new Date(enrollment.event_starts_at).toLocaleString()}</p>
              <p><strong>Status:</strong> {enrollment.status}</p>
              {activeTab === 'upcoming' && enrollment.status === 'enrolled' && (
                <button
                  className="btn btn-danger"
                  onClick={() => handleCancel(enrollment.id)}
                  style={{ marginTop: '15px' }}
                >
                  Cancel Enrollment
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default MyEnrollments

