import React, { useState } from 'react';

function ResetPasswordForm() {
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await fetch('/reset-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email }),
    });
    const data = await response.json();
    if (response.ok) {
      setNewPassword(data.new_password);
    } else {
      alert(data.error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email address:</label>
        <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <button type="submit">Reset Password</button>
      {newPassword && <p>Your new password is: {newPassword}</p>}
    </form>
  );
}

export default ResetPasswordForm;
