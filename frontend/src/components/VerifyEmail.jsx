import { useState } from 'react'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import api from '../utils/api'

function VerifyEmail() {
  const location = useLocation()
  const [email, setEmail] = useState(location.state?.email || '')
  const [otp, setOtp] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      await api.post('/auth/verify-email/', { email, otp })
      setSuccess('Email verified successfully! Redirecting to login...')
      setTimeout(() => {
        navigate('/login')
      }, 2000)
    } catch (err) {
      const errorData = err.response?.data
      if (errorData?.otp) {
        setError(Array.isArray(errorData.otp) ? errorData.otp[0] : errorData.otp)
      } else if (errorData?.email) {
        setError(Array.isArray(errorData.email) ? errorData.email[0] : errorData.email)
      } else {
        setError(errorData?.detail || 'Verification failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card" style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h2>Verify Email</h2>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>OTP</label>
          <input
            type="text"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
            required
            maxLength={6}
            placeholder="Enter 6-digit OTP"
          />
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Verifying...' : 'Verify Email'}
        </button>
      </form>
      <p style={{ marginTop: '15px' }}>
        <Link to="/login">Back to Login</Link>
      </p>
    </div>
  )
}

export default VerifyEmail

