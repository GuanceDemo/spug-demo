import React from 'react';
import { observer } from 'mobx-react';
import { Modal, Form, Input, message } from 'antd';
import http from 'libs/http';
import store from './store';

@observer
class ComForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
    }
  }

  handleSubmit = () => {
    this.setState({loading: true});
    const formData = this.props.form.getFieldsValue();
    formData['id'] = store.record.id;
    http.post('/api/config/service/', formData)
      .then(res => {
        message.success('操作成功');
        store.formVisible = false;
        store.fetchRecords()
      }, () => this.setState({loading: false}))
  };

  render() {
    const info = store.record;
    const {getFieldDecorator} = this.props.form;
    const itemLayout = {
      labelCol: {span: 6},
      wrapperCol: {span: 14}
    };
    return (
      <Modal
        visible
        width={800}
        maskClosable={false}
        title={store.record.id ? '编辑服务' : '新建服务'}
        onCancel={() => store.formVisible = false}
        confirmLoading={this.state.loading}
        onOk={this.handleSubmit}>
        <Form>
          <Form.Item {...itemLayout} required label="服务名称">
            {getFieldDecorator('name', {initialValue: info['name']})(
              <Input placeholder="请输入服务名称，例如：订单处理服务"/>
            )}
          </Form.Item>
          <Form.Item {...itemLayout} required label="唯一标识符">
            {getFieldDecorator('key', {initialValue: info['key']})(
              <Input placeholder="请输入唯一标识符，例如：api_order"/>
            )}
          </Form.Item>
          <Form.Item {...itemLayout} label="备注信息">
            {getFieldDecorator('desc', {initialValue: info['desc']})(
              <Input.TextArea placeholder="请输入备注信息"/>
            )}
          </Form.Item>
        </Form>
      </Modal>
    )
  }
}

export default Form.create()(ComForm)