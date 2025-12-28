import { Link } from 'react-router-dom'

function Navbar({ user, onLogout }) {
  return (
    <nav>
      <div className="container">
        <div>
          <Link to="/">Events Platform</Link>
        </div>
        <div>
          {user?.role === 'Facilitator' && (
            <>
              <Link to="/events/new">Create Event</Link>
              <Link to="/events">My Events</Link>
            </>
          )}
          {user?.role === 'Seeker' && (
            <>
              <Link to="/events">Browse Events</Link>
              <Link to="/my-enrollments">My Enrollments</Link>
            </>
          )}
          <span style={{ margin: '0 10px' }}>{user?.email}</span>
          <button className="btn btn-secondary" onClick={onLogout}>Logout</button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

