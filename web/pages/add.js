import React from 'react'
import { Form, Icon, Input, Button } from 'antd'
import Link from 'next/link'
import { useRouter } from 'next/router'
import axios from 'axios'
import env from '../config/env'

const NormalLoginForm = (props) => {
  const router = useRouter()
  const handleSubmit = async (e) => {
    e.preventDefault()
    props.form.validateFields(async (err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)
        const res = await axios.post(`${env.SERVER_API_URL}/data`, values)
        router.push('/')
      }
    })
  }

  const formItemLayout = {
    labelCol: {
      xs: { span: 6 }
    },
    wrapperCol: {
      xs: { span: 18 }
    }
  }

  const { getFieldDecorator } = props.form
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        maxWidth: 500,
        margin: 'auto',
        minHeight: '95vh'
      }}
    >
      <div style={{ width: 500 }}>
        <h1>Add new csv</h1>
        <Form onSubmit={handleSubmit}>
          <Form.Item label='Title' {...formItemLayout}>
            {getFieldDecorator('label', {
              rules: [{ required: true, message: 'Please input Title!' }]
            })(
              <Input
                prefix={<Icon type='user' style={{ color: 'rgba(0,0,0,.25)' }} />}
                placeholder='Title'
              />
            )}
          </Form.Item>
          <Form.Item label='Google Drive ID' {...formItemLayout}>
            {getFieldDecorator('g_drive_id', {
              rules: [{ required: true, message: 'Please input Google Drive ID!' }]
            })(
              <Input
                prefix={<Icon type='lock' style={{ color: 'rgba(0,0,0,.25)' }} />}
                placeholder='Google Drive ID'
              />
            )}
          </Form.Item>
          <Form.Item>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <Link href='/'>
                <Button type='primary' htmlType='submit'>
              Back
                </Button>
              </Link>
              <Button type='primary' htmlType='submit'>
              Add
              </Button>
            </div>
          </Form.Item>
        </Form>
      </div>
    </div>
  )
}

export default Form.create()(NormalLoginForm)
