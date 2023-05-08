import React from "react";

function DateTime() {
  const showdate = new Date();
  const dt = showdate.toDateString();
  const displaytime = `${showdate.getHours()}:${showdate.getMinutes()}:${showdate.getSeconds()}`;
  return (
    <div>
      {dt} - {displaytime}
    </div>
  );
}

export default DateTime;
