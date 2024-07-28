
import http from "k6/http";
import {sleep} from "k6";

export const options = {
    insecureSkipTlsVerify: true,
    noConnectionReuse: false,
    vus: 1,
    duration: '10s'
};

export default function () {
    const response = http.get("http://localhost:8080/lake/lake/client");
    sleep(1);
}