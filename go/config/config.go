package config

import "os"

type dBConfig struct {
	Host     string
	Port     string
	User     string
	Password string
	DBName   string
}

type authConfig struct {
	SecretKey string
	ExpiresIn string
}

type envConfig struct {
	Env string
}

type Config struct {
	DBConfig   dBConfig
	AuthConfig authConfig
	EnvConfig  envConfig
}

func getEnv(key, defaultVal string) string {
	env := os.Getenv(key)
	if env == "" {
		return defaultVal
	}
	return env
}

func NewConfig() *Config {
	return &Config{
		DBConfig: dBConfig{
			Host:     getEnv("DB_HOST", "localhost"),
			Port:     getEnv("DB_PORT", "5432"),
			User:     getEnv("DB_USER", "postgres"),
			Password: getEnv("DB_PASSWORD", "postgres"),
			DBName:   getEnv("DB_NAME", "postgres"),
		},
		AuthConfig: authConfig{
			SecretKey: getEnv("JWT_SECRET", "secret"),
			ExpiresIn: getEnv("JWT_EXPIRES_DURATION", "60"),
		},
		EnvConfig: envConfig{
			Env: getEnv("ENV", "development"),
		},
	}
}
