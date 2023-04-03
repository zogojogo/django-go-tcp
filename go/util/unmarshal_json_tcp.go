package util

import (
	"encoding/json"
	"fmt"
)

func UnmarshalJSONData(data interface{}, target interface{}) error {
	jsonData, err := json.Marshal(data)
	if err != nil {
		return fmt.Errorf("error marshalling data: %w", err)
	}
	var dataMap map[string]interface{}
	if err := json.Unmarshal(jsonData, &dataMap); err != nil {
		return fmt.Errorf("error unmarshalling data: %w", err)
	}
	if err := json.Unmarshal(jsonData, target); err != nil {
		return fmt.Errorf("error unmarshalling data: %w", err)
	}
	return nil
}
