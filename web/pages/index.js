import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Modal, Spin, Icon, Button } from 'antd'
import Link from 'next/link'
import ReactTable from 'react-table-6'
import Head from 'next/head'
import env from '../config/env'

const parseJSON = (data) => {
  try {
    return JSON.parse(data)
  } catch (error) {
    return data
  }
}
const antIcon = <Icon type='loading' style={{ fontSize: 24 }} spin />
const Home = () => {
  const [data, setData] = useState([])
  const [currentData, setCurrentData] = useState({})
  const [showModal, setShowModal] = useState(false)
  const onClickShowData = (data) => {
    setShowModal(true)
    setCurrentData(data)
  }
  const fetchData = async () => {
    const result = await axios.get(`${env.SERVER_API_URL}/analyze`)
    const data = Object.entries(result.data).map(([key, value]) => {
      const dataformat = {
        detail: value.pending ? 'processing data' : value.data ? 'summarize' : value.error_message,
        title: value.title,
        status: value.pending ? <Spin indicator={antIcon} /> : value.error ? 'Fail' : 'Success',
        g_drive_id: value.g_drive_id
      }
      if (value.data) {
        const data = {
          ...value.data,
          daily_message: parseJSON(value.data.daily_message)
        }
        dataformat.data = data
      }
      return dataformat
    })
    setData(data)
  }
  useEffect(() => {
    fetchData()
  }, [])
  const columns = [{
    Header: 'Title',
    accessor: 'title'
  }, {
    Header: 'DRIVE ID',
    accessor: 'g_drive_id'
  }, {
    Header: 'Status',
    accessor: 'status'
  }, {
    Header: 'Detail',
    accessor: 'detail',
    Cell: props => {
      if (props.value === 'summarize') {
        return <Button onClick={() => onClickShowData(props.original.data)}>Summarize</Button>
      }
      return <span className='number'>{props.value}</span>
    }
  }]
  return (
    <div>
      <Head>
        <title>Social Dashboard</title>
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 20 }}>Social Dashboard</h1>
        <Link href='/add'>
          <Button type='primary' size='large'>
          Add new dataset
            <Icon type='upload' />
          </Button>
        </Link>
      </div>
      <ReactTable
        data={data}
        columns={columns}

      />
      <Modal
        title='Basic Modal'
        visible={showModal}
        onOk={() => setShowModal(false)}
        onCancel={() => setShowModal(false)}
        width='90%'
      >
        <h2>Number of daily messages</h2>
        <table style={{ marginBottom: 50, width: '100%' }}>
          <tr>
            <th>Date</th>
            <th>Date count</th>
          </tr>
          {
            Array.isArray(currentData.daily_message) && currentData.daily_message.map(i => (
              <tr>
                {
                  i.map(j => (
                    <td style={{ width: '48%' }}>{j}</td>
                  ))
                }
              </tr>
            ))
          }
        </table>

        <h2>Top 10 accounts by messages</h2>
        <table style={{ marginBottom: 50, width: '100%' }}>
          <tr>
            <th>Message</th>
            <th>Engagements</th>
          </tr>
          {
            Array.isArray(currentData.top_messages_engagements) && currentData.top_messages_engagements.map(i => (
              <tr>
                {
                  i.map(j => (
                    <td style={{ width: '48%' }}>{j}</td>
                  ))
                }
              </tr>
            ))
          }
        </table>

        <h2>Top 10 accounts by messages</h2>
        <table style={{ marginBottom: 50, width: '100%' }}>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>count</th>
          </tr>
          {
            Array.isArray(currentData.top_accounts) && currentData.top_accounts.map(i => (
              <tr>
                {
                  i.map(j => (
                    <td style={{ width: '30%' }}>{j}</td>
                  ))
                }
              </tr>
            ))
          }
        </table>
      </Modal>
      {/* <style jsx>{`
        .hero {
          width: 100%;
          color: #333;
        }
        .title {
          margin: 0;
          width: 100%;
          padding-top: 80px;
          line-height: 1.15;
          font-size: 48px;
        }
        .title,
        .description {
          text-align: center;
        }
        .row {
          max-width: 880px;
          margin: 80px auto 40px;
          display: flex;
          flex-direction: row;
          justify-content: space-around;
        }
        .card {
          padding: 18px 18px 24px;
          width: 220px;
          text-align: left;
          text-decoration: none;
          color: #434343;
          border: 1px solid #9b9b9b;
        }
        .card:hover {
          border-color: #067df7;
        }
        .card h3 {
          margin: 0;
          color: #067df7;
          font-size: 18px;
        }
        .card p {
          margin: 0;
          padding: 12px 0 0;
          font-size: 13px;
          color: #333;
        }
      `}</style> */}
    </div>
  )
}

export default Home
