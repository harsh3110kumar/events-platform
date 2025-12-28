import { Link } from 'react-router-dom'

function Dashboard({ user }) {
  return (
    <div>
      <h1>Welcome, {user.email}!</h1>
      <div className="card">
        <p><strong>Role:</strong> {user.role}</p>
        <p><strong>Email Verified:</strong> {user.is_email_verified ? 'Yes' : 'No'}</p>
      </div>

      {user.role === 'Facilitator' && (
        <div style={{ marginTop: '20px' }}>
          <Link to="/events/new" className="btn btn-primary">Create New Event</Link>
          <Link to="/events" className="btn btn-secondary" style={{ marginLeft: '10px' }}>View My Events</Link>
        </div>
      )}

      {user.role === 'Seeker' && (
        <div style={{ marginTop: '20px' }}>
          <Link to="/events" className="btn btn-primary">Browse Events</Link>
          <Link to="/my-enrollments" className="btn btn-secondary" style={{ marginLeft: '10px' }}>My Enrollments</Link>
        </div>
      )}
    </div>
  )
}

export default Dashboard

