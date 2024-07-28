
import http from "k6/http";
import {sleep} from "k6";

export const options = {
    insecureSkipTlsVerify: true,
    noConnectionReuse: false,
    vus: 1,
    duration: '10s'
};
const data = JSON.stringify(JSON.parse(open('./data.json')));
export default function () {
    console.log(data)
    const response = http.post("http://localhost:8080/lake/lake/client",data,{
    headers: { 'Content-Type': 'application/json' },
  });
}