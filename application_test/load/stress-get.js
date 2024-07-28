// k6 run stress-get.js
import http from "k6/http";
import {sleep,check} from "k6";

export const options = {
    insecureSkipTlsVerify: true,
    noConnectionReuse: false,
    executor: 'ramping-arrival-rate', //Assure load increase if the system slows
      stages: [
        { duration: '60s', target: 400 }, // just slowly ramp-up to a HUGE load
      ],
};

export default function () {
    const response = http.get("http://localhost:80/lake/lake/client");
    check(response, { 'success': (r) => r.status === 200 })
}