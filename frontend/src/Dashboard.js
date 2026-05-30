import React, {useEffect, useState} from 'react';

function Dashboard() {
    const[alerts, setAlerts] = useState([]);

    const fetchAlerts = async () => {
        const res=await
            fetch("http://127.0.0.1.5000/api/alerts");
            const data =await res.json();
            setAlerts(data);
    };
    const dismissAlert = async (id) => {
        await fetch(`http://127.0.0.1.5000/api/alerts/${id}`, { method: 'DELETE' });
        fetchAlerts(); 
    };
    useEffect(() => {
        fetchAlerts();

        const interval = setInterval(fetchAlerts, 5000);
        return () => clearInterval(interval);
    }, []);

        return (
            <div>
                <h1>Dashboard</h1>
                {alerts.length === 0 ? (
                    <p>No active alerts</p>
                ) : (
                alerts.map((alert, index) => (
                    <div 
                    key={index} 
                    style={{ 
                        border: '1px solid black', 
                        margin: '10px', 
                        padding: '10px' }}
                    >
                        <p>Device: {alert.device_id}</p>
                        <p>Type: {alert.metric}</p>
                        <p>Value: {alert.value}</p>
                        <button onClick={() => dismissAlert(index)}>Dismiss</button>
                    </div>
                ))
            )}
            </div>
        );
    }
    export default Dashboard;
