package util

import (
	"encoding/json"
	"entry_task/dto"
	"entry_task/pb"
	"fmt"
	"net"

	"github.com/golang/protobuf/ptypes/any"
	"google.golang.org/protobuf/proto"
)

func ResponseSuccessJSON(statusCode int, data interface{}, encoder *json.Encoder) error {
	response := dto.TCPResponseDTO{
		Code: statusCode,
		Data: data,
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}

func ResponseErrorJSON(statusCode int, err error, encoder *json.Encoder) error {
	response := dto.TCPResponseDTO{
		Code:    statusCode,
		Message: err.Error(),
	}
	if err := encoder.Encode(response); err != nil {
		return err
	}
	return nil
}

func WriteSuccessTCPResponse(conn net.Conn, code int32, data *any.Any) error {
	tcpResponse := &pb.TCPResponse{
		Code: code,
		Data: data,
	}

	responseBytes, err := proto.Marshal(tcpResponse)
	if err != nil {
		return fmt.Errorf("failed to marshal TCP response: %v", err)
	}

	_, err = conn.Write(responseBytes)
	if err != nil {
		return fmt.Errorf("failed to write TCP response: %v", err)
	}

	return nil
}

func WriteErrorTCPResponse(conn net.Conn, code int32, message string) error {
	tcpResponse := &pb.TCPResponse{
		Code:    code,
		Message: message,
	}

	responseBytes, err := proto.Marshal(tcpResponse)
	if err != nil {
		return fmt.Errorf("failed to marshal TCP response: %v", err)
	}

	_, err = conn.Write(responseBytes)
	if err != nil {
		return fmt.Errorf("failed to write TCP response: %v", err)
	}

	return nil
}
