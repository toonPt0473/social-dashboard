import App, { Container } from 'next/app'
import Head from 'next/head'
import React from 'react'

import 'antd/dist/antd.css'

class MyApp extends App {
  static async getInitialProps ({ Component, ctx }) {
    return {
      pageProps: {
        ...(Component.getInitialProps ? await Component.getInitialProps(ctx) : {})
      }
    }
  }

  render () {
    const { Component, pageProps } = this.props

    return (
      <Container>
        <Head>
          <title>Social Dashboard</title>
          <link
            rel='stylesheet'
            href='https://unpkg.com/react-table-6@latest/react-table.css'
          />
        </Head>
        <Component {...pageProps} />
      </Container>
    )
  }
}

export default MyApp
